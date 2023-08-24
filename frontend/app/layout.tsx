
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import "./../styles/reset.css"
import "./../styles/style.css"
import TheHeader from '@/components/TheHeader/TheHeader'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Buyme',
  description: 'Buyme - ethernet shop',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <TheHeader />
        {children}
        </body>
    </html>
  )
}
