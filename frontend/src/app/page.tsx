import ChatWindow from "@/components/chat/ChatWindow";
import WishlistButton from "@/components/wishlist/WishlistButton";

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen bg-bg-primary">
      <ChatWindow />
      <WishlistButton />
    </main>
  );
}
