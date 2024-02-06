'use client'
import { useMemo, useEffect, useState } from "react";

import Facts from './facts';

interface RosterEntry {
  name: string
  team: string
  score: number
}

function Roster(props: any) {
  const roster: RosterEntry[] = props.roster;

  const rosterEl = roster.map(({ name, team, score }) => {
    return (<li key={name}><code>{score}</code> {name} <i>{team}</i></li>);
  });
  const score = roster.reduce(((sum, { score }) => sum + score), 0);

  return (
    <>
      <p>
        <code><b>{score}</b></code> / {props.target}
      </p>
      <ol>{rosterEl}</ol>
    </>
  );
}


function Form(props: any) {
  const { updateRoster, currentRound, currentTeam, rounds, suggestions } = props;

  const [currentName, setCurrentName] = useState('')
  const onInput = (e: any) => {
    setCurrentName(e.target.value);
  }

  const onSubmit = (e: any) => {
    e.preventDefault();
    if (!suggestions.includes(currentName)) { return; }
    const ok = updateRoster(currentName);
    if (ok) { setCurrentName(''); }
  }
  const optsEl = (suggestions || []).map((s: string) => {
    return (<option key={s}>{s}</option>)
  });

  return (
    <>
      <span>{currentRound}/{rounds}. {currentTeam}</span>
      <form onSubmit={onSubmit} autoComplete="off">
        <input id="current" list="optList" type="text" value={currentName} onInput={onInput} />
        <datalist id="optList">
          {optsEl}
        </datalist>
        <input type="submit" value="Submit" />
      </form>
    </>
  );
}

export default function Game(props: any) {

  const { rounds, target } = props;
  const facts = new Facts(props.facts);


  const [roster, setRoster] = useState(([] as RosterEntry[]));

  const [currentTeam, setCurrentTeam] = useState('')
  const [currentRound, setCurrentRound] = useState(1)

  useEffect(() => setCurrentTeam(facts.randomTeam()), []);

  const score = roster.reduce(((sum, { score }) => sum + score), 0);
  const isWin = score > target;
  const isDone = currentRound > rounds;

  const updateRoster = (name: string) => {

    const score = (facts.validForTeam(name, currentTeam) ? facts.score(name) : 0);

    const newEntry = {
      name: name,
      team: currentTeam,
      score: score,
    }

    setRoster([...roster, newEntry]);
    setCurrentTeam(facts.randomTeam())
    setCurrentRound(currentRound + 1)
    return true;
  }

  const suggestions = useMemo(() => facts.allPlayers(), [facts])

  return (
    <>
      {isDone ?
        (<big>{isWin ? "✅ win! ✅" : "❌ lose! ❌"}</big>) :
        (<Form currentTeam={currentTeam} currentRound={currentRound} rounds={rounds} updateRoster={updateRoster} suggestions={suggestions} />)
      }
      <Roster roster={roster} target={target} />
    </>
  )
}



