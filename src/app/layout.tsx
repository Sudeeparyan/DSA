import type { Metadata, Viewport } from "next";
import Link from "next/link";
import { DM_Sans, IBM_Plex_Mono } from "next/font/google";
import { ServiceWorkerRegister } from "@/components/layout/ServiceWorkerRegister";
import "./globals.css";
import "./lesson.css";

const body = DM_Sans({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-code",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: {
    default: "NeetCode 150, step by step",
    template: "%s · NeetCode 150, step by step",
  },
  description:
    "Understand every NeetCode 150 problem: the question in plain words, the key idea, and a 3D walkthrough of the real solution running line by line.",
  manifest: "/manifest.webmanifest",
  appleWebApp: { capable: true, title: "NeetCode 150" },
};

export const viewport: Viewport = {
  themeColor: "#0b1018",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // the font variables live on <html> so that :root-level CSS variables can use them
    <html lang="en" className={`${body.variable} ${mono.variable}`}>
      <body>
        <ServiceWorkerRegister />
        <header className="site-head">
          {/* one inner span: a flex item trims the spaces at its edges, which ate the one after "NeetCode" */}
          <Link href="/" className="site-name">
            <span>
              NeetCode <span className="site-accent">150</span>, step by step
            </span>
          </Link>
          <Link href="/" className="site-link">
            All problems
          </Link>
        </header>
        <main>{children}</main>
        <footer className="site-foot">
          A study aid for the NeetCode 150 list. Not affiliated with NeetCode or LeetCode.
        </footer>
      </body>
    </html>
  );
}
