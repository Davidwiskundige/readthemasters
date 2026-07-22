import { defineConfig } from "astro/config";

// Static site. `site` is the Cloudflare Pages project URL until a custom domain is attached
// (see .github/workflows/ci.yml deploy step) — update here once a real domain is in place.
export default defineConfig({
  site: "https://readthemasters.pages.dev",
  build: { format: "directory" },
});
