import Link from 'next/link';
import game_configs from './game/[slug]/data/games.json';
export default function Home() {

    const rows = Object.keys(game_configs).map(slug => {
        const { title, rounds, target } = (game_configs as any)[slug];
        return (
            <tr key={slug}>
                <td>
                    <Link href={`game/${slug}`}>{title}</Link>
                </td>
                <td>{rounds}</td>
                <td>{target}</td>
            </tr>
        )
    })

    return (
        <table>
            <thead><tr>
                <th>game</th>
                <th>rounds</th>
                <th>target</th>
            </tr></thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    )
}