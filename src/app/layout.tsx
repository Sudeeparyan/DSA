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
  title: "NeetCode 150 Learn",
  description:
    "Kid-simple animated explanations of all NeetCode 150 problems for Google interview prep.",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    title: "NC150 Learn",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#e7eef5" },
    { media: "(prefers-color-scheme: dark)", color: "#070b12" },
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
          <footer className="mx-auto max-w-6xl px-4 py-12 text-sm text-muted">
            <div className="brand-font text-base text-foreground">
              NeetCode<span className="text-accent">150</span> Learn
            </div>
            <p className="mt-2 max-w-xl">
              Offline-friendly study companion for Google interview prep. Not
              affiliated with NeetCode or LeetCode.
            </p>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
