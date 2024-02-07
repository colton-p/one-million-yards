import Link from 'next/link';
import game_configs from './game/[slug]/data/games.json';
import { redirect } from "next/navigation";

export default function Home() {
    return redirect('/game/nfl-pass_yds-20')
}