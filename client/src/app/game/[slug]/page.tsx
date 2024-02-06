import Image from "next/image";
import styles from "./page.module.css";
import Game from "./game";
import Facts from "./facts";
import data from './data/mlb-hr.json';
import game_configs from './data/games.json';

export function generateStaticParams() {
  console.log( Object.keys(game_configs).map(slug => ({slug})))
  return Object.keys(game_configs).map(slug => ({slug}));
}



export default function Home({ params }: { params: { slug: string } }) {
  const { title, rounds, target, data_file } = (game_configs as any)[params.slug];
  const data = require(`./data/${data_file}`)
  return (
    <>
      <h4>{title}</h4>
      <div>
        <Game facts={data} rounds={rounds} target={target}/>
      </div>
    </>
  );
}
