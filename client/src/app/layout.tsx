import type { Metadata } from "next";
import Link from "next/link";

import 'simpledotcss/simple.css'

export const metadata: Metadata = {
  title: "1 Million Yards",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
      </head>
      <body>
        {children}
        <footer>
          <Link href="/game">other games</Link> |&nbsp;
          <Link href="/about">about</Link> |&nbsp;
          <Link href="https://github.com/colton-p/one-million-yards">github</Link>
        </footer>
      </body>
    </html>
  );
}
