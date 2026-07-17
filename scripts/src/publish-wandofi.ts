import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join, relative } from "node:path";

const OWNER = "Wandofi";
const REPO = "wandofi-website";
const BRANCH = "gh-pages";
const SITE_URL = "https://wandofi.pt/";
const ROOT = join(import.meta.dirname, "..", "..");
const ARTIFACT_DIR = join(ROOT, "artifacts", "wandofi");
const DIST_DIR = join(ARTIFACT_DIR, "dist", "public");

function fail(msg: string): never {
  console.error(`✗ ${msg}`);
  process.exit(1);
}

async function getGithubToken(): Promise<string> {
  const hostname = process.env.REPLIT_CONNECTORS_HOSTNAME;
  const identity = process.env.REPL_IDENTITY
    ? `repl ${process.env.REPL_IDENTITY}`
    : process.env.WEB_REPL_RENEWAL
      ? `depl ${process.env.WEB_REPL_RENEWAL}`
      : null;
  if (!hostname || !identity) fail("Replit connector environment not available (REPLIT_CONNECTORS_HOSTNAME / REPL_IDENTITY).");

  // Deliberately no connector_names filter: it can return 0 items even when
  // the connection is healthy. List all and pick the GitHub connection.
  const res = await fetch(`https://${hostname}/api/v2/connection?include_secrets=true`, {
    headers: { Accept: "application/json", X_REPLIT_TOKEN: identity },
  });
  if (!res.ok) fail(`Connector API returned ${res.status}`);
  const data = (await res.json()) as { items?: Array<Record<string, any>> };
  const conn = (data.items ?? []).find((c) => typeof c.id === "string" && c.id.startsWith("conn_github"));
  if (!conn) fail("No GitHub connection found. Connect GitHub in the Replit integrations panel.");
  const token: string | undefined =
    conn.settings?.access_token ?? conn.settings?.oauth?.credentials?.access_token;
  if (!token) fail("GitHub connection has no access token.");
  return token;
}

function buildSite(): void {
  console.log("→ Building production site…");
  execFileSync("pnpm", ["--filter", "@workspace/wandofi", "run", "build"], {
    cwd: ROOT,
    stdio: "inherit",
    env: { ...process.env, PORT: "3000", BASE_PATH: "/", NODE_ENV: "production" },
  });
  if (!existsSync(join(DIST_DIR, "index.html"))) fail(`Build output missing at ${DIST_DIR}`);
}

function collectFiles(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) out.push(...collectFiles(full));
    else out.push(full);
  }
  return out;
}

async function gh(token: string, method: string, path: string, body?: unknown): Promise<any> {
  const res = await fetch(`https://api.github.com${path}`, {
    method,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${token}`,
      "X-GitHub-Api-Version": "2022-11-28",
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const text = await res.text();
    fail(`GitHub API ${method} ${path} → ${res.status}: ${text.slice(0, 300)}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

async function publish(token: string, stampId: string): Promise<void> {
  const files = collectFiles(DIST_DIR).map((abs) => ({
    path: relative(DIST_DIR, abs).split("\\").join("/"),
    abs,
  }));

  const paths = new Set(files.map((f) => f.path));
  if (!paths.has("CNAME")) fail("CNAME missing from build output — wandofi.pt would break.");

  console.log(`→ Uploading ${files.length + 1} files to ${OWNER}/${REPO}@${BRANCH}…`);

  const tree: Array<{ path: string; mode: string; type: string; sha: string }> = [];
  for (const file of files) {
    const blob = await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/blobs`, {
      content: readFileSync(file.abs).toString("base64"),
      encoding: "base64",
    });
    tree.push({ path: file.path, mode: "100644", type: "blob", sha: blob.sha });
  }
  // .nojekyll so GitHub Pages serves files as-is
  const nojekyll = await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/blobs`, {
    content: "",
    encoding: "base64",
  });
  tree.push({ path: ".nojekyll", mode: "100644", type: "blob", sha: nojekyll.sha });
  // Unique per-deploy stamp so verification can prove the NEW build is live
  const stamp = await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/blobs`, {
    content: Buffer.from(stampId, "utf8").toString("base64"),
    encoding: "base64",
  });
  tree.push({ path: "deploy-stamp.txt", mode: "100644", type: "blob", sha: stamp.sha });

  const treeObj = await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/trees`, { tree });
  const commit = await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/commits`, {
    message: `Publish wandofi.pt (${new Date().toISOString()})`,
    tree: treeObj.sha,
    parents: [],
  });

  // Force-update (or create) the gh-pages ref
  const refPath = `/repos/${OWNER}/${REPO}/git/refs/heads/${BRANCH}`;
  const refRes = await fetch(`https://api.github.com${refPath}`, {
    headers: { Accept: "application/vnd.github+json", Authorization: `Bearer ${token}` },
  });
  if (refRes.ok) {
    await gh(token, "PATCH", refPath, { sha: commit.sha, force: true });
  } else {
    await gh(token, "POST", `/repos/${OWNER}/${REPO}/git/refs`, {
      ref: `refs/heads/${BRANCH}`,
      sha: commit.sha,
    });
  }
  console.log(`✓ Pushed commit ${commit.sha.slice(0, 7)} to ${BRANCH}`);

  // Request a Pages build (ignore 409 "already building" style failures gracefully)
  const buildRes = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/pages/builds`, {
    method: "POST",
    headers: { Accept: "application/vnd.github+json", Authorization: `Bearer ${token}` },
  });
  if (!buildRes.ok && buildRes.status !== 409) {
    console.warn(`  (Pages build request returned ${buildRes.status}; GitHub usually builds automatically on push.)`);
  }
}

async function verify(stampId: string): Promise<void> {
  const expected = readFileSync(join(DIST_DIR, "index.html"), "utf8");
  console.log("→ Verifying https://wandofi.pt/ serves the new build…");
  const deadline = Date.now() + 5 * 60 * 1000;
  let lastState = "no response yet";
  while (Date.now() < deadline) {
    try {
      // 1) The unique per-deploy stamp proves the NEW deploy is live (not a stale cache).
      const stampRes = await fetch(`${SITE_URL}deploy-stamp.txt?v=${Date.now()}`, {
        headers: { "Cache-Control": "no-cache" },
        redirect: "follow",
      });
      if (stampRes.status !== 200 || (await stampRes.text()).trim() !== stampId) {
        lastState = `deploy stamp not live yet (status ${stampRes.status})`;
      } else {
        // 2) The homepage must return 200 with exactly the freshly built HTML.
        const res = await fetch(`${SITE_URL}?v=${Date.now()}`, {
          headers: { "Cache-Control": "no-cache" },
          redirect: "follow",
        });
        if (res.status === 200 && (await res.text()) === expected) {
          console.log("✓ https://wandofi.pt/ returns 200 with the new content. Publish complete.");
          return;
        }
        lastState = `stamp live, but homepage not matching new build yet (status ${res.status})`;
      }
    } catch (err) {
      lastState = `network error: ${(err as Error).message}`;
    }
    await new Promise((r) => setTimeout(r, 10_000));
  }
  fail(`Timed out waiting for wandofi.pt to serve the new build (${lastState}). The push succeeded; the Pages CDN may still be propagating — check again in a few minutes.`);
}

const stampId = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
const token = await getGithubToken();
buildSite();
await publish(token, stampId);
await verify(stampId);
