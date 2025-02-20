import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Filter } from "lucide-react"

export function SearchBar() {
  return (
    <div className="flex gap-2 p-4">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
        <Input className="pl-9" placeholder="検索" />
      </div>
      <Button variant="outline">
        <Filter className="mr-2 h-4 w-4" />
        フィルター
      </Button>
    </div>
  )
}

