import Dashboard from "./(dashboard)/page";
import Header from "./components/Header/Header";
export default function Home() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center bg-background font-sans text-foreground">
      <Header />
      <main className="flex w-full flex-1 flex-col items-center bg-background px-16 py-10 sm:items-start">
        <Dashboard />
      </main>
    </div>
  );
}
