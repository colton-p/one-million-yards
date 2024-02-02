
const pick = (arr: any) => arr[Math.floor(Math.random() * arr.length)]

export default class Facts {
    teams: string[]
    players: any
    scores: any

    constructor(data: any) {
        this.teams = data.teams;
        this.players = data.players;
        this.scores = data.scores;
    }

    randomTeam() {
        return pick(this.teams);
    }

    score(player: string) {
        return this.scores[player] || 0;
    }

    validForTeam(player: string, team: string) {
        return this.players[team].includes(player);
    }

    allPlayers() {
        const all = Object.values(this.players).flatMap(a => a)
        const uniq = Array.from(new Set(all));

        return uniq.sort();
    }
}