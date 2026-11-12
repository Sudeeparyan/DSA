import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Page not found" };

export default function NotFound() {
  return (
    <div className="home">
      <header className="home-head">
        <h1>That page does not exist</h1>
        <p>The link may be mistyped, or the page may have moved. Every problem is listed on the home page.</p>
        <div className="home-actions">
          <Link href="/" className="btn btn-primary">
            See all problems
          </Link>
        </div>
      </header>
    </div>
  );
}
