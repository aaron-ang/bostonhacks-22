import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/router";
import { MouseEvent, useState } from "react";

const Dashboard = () => {
  const router = useRouter();
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      router.push("/");
    },
  });

  const [number, setNumber] = useState("");
  const user = session?.user;

  const handleSignOut = (e: MouseEvent<HTMLButtonElement>) => {
    e.currentTarget.innerText = "Logging out...";
    signOut({ callbackUrl: "/" });
  };

  const updateNumber = (e: MouseEvent<HTMLButtonElement>) => {
    // e.currentTarget.innerText = "Updating...";
    e.preventDefault();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNumber(e.target.value);
  };

  return (
    <>
      <h1>Hello, {user?.name}</h1>
      <input
        type="tel"
        pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
        placeholder="123-456-7890"
        onChange={handleChange}
      ></input>
      <button onClick={updateNumber}>Update Number</button>
      <div>
        <button onClick={handleSignOut}>Log Out</button>
      </div>
    </>
  );
};

export default Dashboard;
