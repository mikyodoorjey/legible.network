// Vercel Edge Middleware: Basic Auth over the whole site until launch.
// Env: the site is locked unless SITE_LOCKED=0. SITE_USER / SITE_PASSWORD for the preview login,
// PUBLIC_PATHS as a comma-separated list of path prefixes that stay open (e.g. /rubric/,/about/,/assets/).
// Set SITE_LOCKED=0 and redeploy to open the site. Unset means locked (fail closed).

export const config = { matcher: ["/((?!favicon.svg|robots.txt).*)"] };

function timingSafeEqual(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(a), y = enc.encode(b);
  let diff = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) diff |= (x[i] ?? 0) ^ (y[i] ?? 0);
  return diff === 0;
}

function challenge(status, body) {
  return new Response(body, {
    status,
    headers: {
      "WWW-Authenticate": 'Basic realm="legible.network preview", charset="UTF-8"',
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

export default function middleware(request) {
  if (process.env.SITE_LOCKED === "0") return;
  const pathname = new URL(request.url).pathname;
  const open = (process.env.PUBLIC_PATHS || "").split(",").map(s => s.trim()).filter(Boolean);
  if (open.some(p => pathname === p || pathname.startsWith(p))) return;

  const password = process.env.SITE_PASSWORD;
  const user = process.env.SITE_USER || "preview";
  if (!password) return challenge(503, "This site is locked and no preview password has been set yet.");

  const header = request.headers.get("authorization") || "";
  if (header.startsWith("Basic ")) {
    let decoded = "";
    try { decoded = atob(header.slice(6)); } catch (e) { decoded = ""; }
    const i = decoded.indexOf(":");
    const u = i >= 0 ? decoded.slice(0, i) : "";
    const p = i >= 0 ? decoded.slice(i + 1) : "";
    if (timingSafeEqual(u, user) && timingSafeEqual(p, password)) return;
  }
  return challenge(401, "The Subnet Legibility Index publishes September 21. Sign in for the preview.");
}
