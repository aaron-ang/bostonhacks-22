import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/router";
import { MouseEvent, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const router = useRouter();
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      router.push("/");
    },
  });

  const [number, setNumber] = useState("");
  const [updating, setUpdating] = useState(false);
  const user = session?.user;
  const email = user?.email;

  const handleSignOut = (e: MouseEvent<HTMLButtonElement>) => {
    e.currentTarget.innerText = "Logging out...";
    signOut({ callbackUrl: "/" });
  };

  const validNumber = (number: string) => {
    const regex = /^[0-9]{3}-[0-9]{3}-[0-9]{4}$/;
    return number.match(regex);
  };

  const updateNumber = (e: MouseEvent<HTMLButtonElement>) => {
    if (!validNumber(number)) {
      alert("Please enter a valid number");
      return;
    }
    setUpdating(true);
    axios
      .post("api/update", { email: email, number: number })
      .then(() => setUpdating(false));
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
      <button onClick={updateNumber}>
        {updating ? "Updating..." : "Update Number"}
      </button>
      <div>
        <button onClick={handleSignOut}>Log Out</button>
      </div>
      {/* <ToastContainer /> */}
    </>
  );
};

export default Dashboard;