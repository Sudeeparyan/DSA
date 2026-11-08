import type { Metadata, Viewport } from "next";
import { Syne, Literata, DM_Sans, IBM_Plex_Mono } from "next/font/google";
import { ThemeProvider } from "@/components/layout/ThemeProvider";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { ServiceWorkerRegister } from "@/components/layout/ServiceWorkerRegister";
import "./globals.css";

const brand = Syne({
  variable: "--font-brand",
  subsets: ["latin"],
  weight: ["600", "700", "800"],
});

const teach = Literata({
  variable: "--font-teach",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

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
  title: "NeetCode 150 Play",
  description:
    "Teacher-led animated lessons for every NeetCode 150 problem — watch the puzzle, explode the idea like a rocket, play the algorithm.",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    title: "NC150 Play",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#070b09" },
    { media: "(prefers-color-scheme: dark)", color: "#070b09" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${brand.variable} ${teach.variable} ${body.variable} ${mono.variable} antialiased`}
      >
        <ThemeProvider>
          <ServiceWorkerRegister />
          <SiteHeader />
          <main>{children}</main>
          <footer className="border-t border-white/10 bg-[#070b09] px-4 py-10 text-sm text-white/45">
            <div className="mx-auto max-w-6xl">
              <div className="brand-font text-base text-white">
                NeetCode<span className="text-accent">150</span> Play
              </div>
              <p className="mt-2 max-w-xl">
                Offline-friendly animated classroom for Google interview prep.
                Not affiliated with NeetCode or LeetCode.
              </p>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
