import Image from "next/image";
import styles from "./page.module.css";
import Game from "./game";
import Facts from "./facts";
import data from './data';

export function generateStaticParams() {
  return ['hello', 'goodbye'].map(slug => ({slug}));
}

export default function Home({ params }: { params: { slug: string } }) {

  return (
    <>
      <h4>passing yards</h4>
      <div>
        <Game facts={data} rounds={5} target={200_000}/>
      </div>
    </>
  );
}
