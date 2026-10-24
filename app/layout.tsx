import type { Metadata } from "next";
import "./globals.css";

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
    >
      <body className="min-h-full flex flex-col h-dvh">{children}</body>
    </html>
  );
}
