import './globals.css'

export const metadata = {
  title: 'Conversation Simulator',
  description: 'A conversation simulation app',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
