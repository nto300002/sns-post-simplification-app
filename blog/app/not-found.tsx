import Link from "next/link"

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">404 - ページが見つかりません</h1>
        <p className="mb-4">お探しのページは存在しないか、移動した可能性があります。</p>
        <Link href="/" className="text-blue-500 hover:underline">
          ホームページに戻る
        </Link>
      </div>
    </div>
  )
}

