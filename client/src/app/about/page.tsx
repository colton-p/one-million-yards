
export default function About() {
    return (
        <>
            <h3>about</h3>
            <span>Goal: accumulate one million yards of career passing yards, over twenty rounds.</span>
                <ul>
                    <li>You will see a series of random NFL teams.</li>
                    <li>Name a quarterback who, at any point, played for that team.</li>
                    <li>Your score is that quarterback&apos;s career passing yardage.
                        <ul>
                            <li>All career yardage counts, even yards gained with other teams (so, for a prompt of either Patriots or Buccaneers, Tom Brady is worth all 89k yards).</li>
                            <li>Relocated teams are treated as the same team (so, for a prompt of &quot;Indianapolis Colts&quot;, the Baltimore Colts&apos; Johnny Unitas is a valid answer).</li>
                        </ul>
                    </li>
                </ul>

            <ul>
                <li>Inspired by the <a href="https://www.tiktok.com/discover/1-million-passing-yards?lang=en">&quot;million passing yards challenge&quot;</a> minor TikTok trend.</li>
                <li>All statistics from the <a href="https://www.sports-reference.com/">Sports Reference</a> family of sites.
                    <ul>
                        <li>Lovingly scraped conforming to the limits in their <a href="https://www.sports-reference.com/bot-traffic.html">bot traffic</a> policy.</li>
                    </ul>
                </li>      
            </ul> </>
    )
}