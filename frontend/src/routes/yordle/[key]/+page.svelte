<svelte:window  on:keydown={handleKeyPress} />

<head>
  <style>
    .button-container {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
    }

    .keyboard {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
    }
    .keyboard-row {
      display: flex;
      justify-content: center;
      width: 100%;
    }

    .key {
      flex: 1;
      /* max-width: 100px; */
      /* max-height: 100px; */
      margin: 5px;
      text-align: center;
      line-height: 40px;
      border: 1px solid #ccc;
      border-radius: 5px;
      cursor: pointer;
      user-select: none;
      transition: background 0.3s;
      background-color: var(--background-color);
      color: var(--text-color);
    }

    .key:hover {
      background: #f0f0f0;
    }
    .key:active {
      background: #ccc;
    }
    @media (max-width: 600px) {
      .key {
        /* max-width: 30px; */
        height: 30px;
        line-height: 30px;
        margin: 3px;
      }
    }
    .header {
      text-align: center;
      margin-top: 20px;
    }
    .wordle-container {
      display: grid;
      align-items: center;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      grid-template-rows: repeat(5, minmax(0, 1fr));
    }


    .score-container {
      grid-area: 1 / 1 / 3 / 2;
    }

    .desktop-view {
      display: block;
    }

    .mobile-view {
      display: none;
    }

    @media (max-width: 600px) {
      .desktop-view {
        display: none;
      }

      .mobile-view {
        display: block;
      }

      .score-container {
        padding-bottom: 10px;
      }

      .wordle-container {
        display: flex;
        flex-direction: column;
      }

      .keyboard {
      flex-direction: column;
      align-items: center;
      }

      .keyboard-row {
      justify-content: center;
      }

      .key {
      height: 30px;
      line-height: 30px;
      margin: 3px;
      }


      .game-container {
      grid-template-rows: 1fr 1fr 4fr;
      }

      .lobby {
      grid-template-rows: 1fr 1fr;
      }
    }
    .wordle-text-container {
      grid-area: 1 / 2 / 3 / 6;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .guess-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

    }

    .summary {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .keyboard {
      grid-area: 3 / 1 / 6 / 6;
      font-family: 'Roboto', sans-serif;

    }

    .game-container {
      display: grid;
      grid-template-rows: 1fr 1fr 4fr;
      align-items: center;
    }

    .lobby {
      display: grid;
      grid-template-rows: 1fr 1fr;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="game-container">
    <Title title="yordle"></Title>
    <div class="button-container">
      <!-- <Fab extended href="/"><Label>Back</Label></Fab>
      <Fab extended on:click={() => { submitAnswer() } }><Label>Submit</Label></Fab> -->

      <Button aria-disabled={state != GameState.ACTIVE} on:click={() => { leaveGame() }}>Leave</Button>
      {#if state == GameState.ACTIVE}
      <Timer secondsLeft={secondsLeft} />
      <br />
      <b>Lvl: {currentIndex+1}</b>
      {:else if state == GameState.WAITING}
      <Button on:click={startGame}>Start</Button>
      {/if}
    </div>
    {#if state === GameState.ACTIVE}
    <div class="wordle-container">
      <div class="score-container">
        <div class="desktop-view">
            <Scoreboard currentPlayerId={clientId} scores={currentScores}></Scoreboard>
        </div>
        <div class="mobile-view">
          <Rank scores={currentScores} currentPlayerId={clientId} />
        </div>
      </div>
      <div class="wordle-text-container">
        <div class="guess-container">
          {#each Object.keys(allCurrentGuesses) as playerId}
            {#if playerId !== clientId && allAnswerLen[playerId] !== undefined}
              <WordleText maxLetters={allAnswerLen[playerId]} text={allCurrentGuesses[playerId]} />
            {/if}
          {/each}          
          <WordleText maxLetters={answerLen} text={currentGuess} />

        </div>
        <WordleHint entries={guessHistory} />
      </div>

      <div class="keyboard">
        {#each rows as row}
        <div class="keyboard-row">
          {#each row as ch}
            {#if ch === "BACKSPACE"}
            <button disabled={state != GameState.ACTIVE} class="key" on:click={() => removeLetter()}>{ch}</button>
            {:else if ch === "ENTER"}
            <button disabled={state != GameState.ACTIVE} class="key" on:click={() => submitAnswer()}>{ch}</button>
            {:else}
            <button disabled={state != GameState.ACTIVE} class="key" on:click={() => addLetter(ch)}>{ch}</button>
            {/if}
          {/each}
        </div>
        {/each}
      </div>
    </div>
    {:else if state === GameState.OVER}
    <div class="summary">
      <h1>Game Over</h1>
      <Scoreboard currentPlayerId={clientId} scores={currentScores}></Scoreboard>
    </div>
    {:else if state === GameState.WAITING}
    <div class="lobby">
      <div class="button-container">
        <Button href="/"></Button>  
      </div>
      <Scoreboard currentPlayerId={clientId} scores={currentScores} />
    </div>
    {:else if state === GameState.STARTING}
    <Countdown delay={5} />
    {:else if state === GameState.INITIALIZING}
    <CircularProgress style="height: 32px; width: 32px;" indeterminate />
    {/if}
</body>

<script>
import websocketStore from "svelte-websocket-store";
import LinearProgress from '@smui/linear-progress';
import CircularProgress from '@smui/circular-progress';


import { onMount,onDestroy, setContext, getContext } from "svelte";
import Title from "$components/title.svelte"
import WordleText from "$components/wordleText.svelte";
import WordleHint from "$components/wordleHint.svelte";
import Countdown from "$components/countdown.svelte";
import Rank from "$components/rank.svelte";
import Button from "@smui/button";
import { Entry } from "$components/types"
import Fab from "@smui/fab";
import { Label } from "@smui/common"
import Score from '$components/score.svelte'
import Scoreboard from "$components/scoreboard.svelte";
import Timer from "$components/timer.svelte";
import Card from "@smui/card";
import { goto } from "$app/navigation";
import { api, websocket } from "stores/url"



export let data;
let gameKey = ""

/**
 * @type {string|undefined}
 */
let clientId;

let currentGuess = ""
let allCurrentGuesses = {}
let currentIndex = 0

let currentScores = {}
let answerLen = 10
let allAnswerLen = {}
let correctPercent = 0.0
let score = 0
let apiURL = api()
let wsURL = websocket()


/**
 * @type {Entry[]}
*/
let guessHistory = []

let rows = [
  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
  ["Z", "X", "C", "V", "B", "N", "M"],
  ["BACKSPACE", "ENTER"]
]


const GameState = {
  ACTIVE: "State.ACTIVE",
  OVER: "State.OVER",
  WAITING: "State.WAITING",
  STARTING: "State.STARTING",
  INITIALIZING: "State.INITIALIZING"
};
/**
 * @type {String}
 */
let state = GameState.WAITING
let secondsLeft = 30

/**
 * @type {WebSocket} socket
 */
let socket;
let closing = false


/**
 * updates the current guess
 * @param {string} guess
 */
let updateGuess = (guess) => {
  currentGuess = guess
}

function updateState(new_state) {
  console.log("new state", new_state)
  console.log("client id", clientId)

  
  if (new_state.answer_len !== undefined) {
    allAnswerLen = new_state.answer_len
    if (allAnswerLen[clientId] !== undefined) {
      answerLen = allAnswerLen[clientId]
      console.log("new answer len", answerLen)
    }
  }

  if (new_state.correct_percent != undefined) {
    correctPercent = new_state.correct_percent
    console.log(correctPercent)
  }


  if (new_state.scores != undefined) {
    if (clientId != undefined && new_state.scores[clientId] != undefined) {
      score = new_state.scores[clientId]
    }
    currentScores = new_state.scores
  }

  if (new_state.guess_history != undefined) {
    guessHistory = new_state.guess_history
  }

  if (new_state.time_left != undefined) {
    secondsLeft = new_state.time_left
  }

  if (new_state.state != undefined) {
    state = new_state.state
  } 

  if (new_state.word_index != undefined && clientId in new_state.word_index) {
    currentIndex = new_state.word_index[clientId]
  }

  if (new_state.current_guess != undefined) {
    allCurrentGuesses = new_state.current_guess
    console.log(allCurrentGuesses)
    if (clientId != undefined && allCurrentGuesses[clientId] != undefined) {
      updateGuess(allCurrentGuesses[clientId])
    }
  }
}

function connect() {
  try {
    console.dir(wsURL)
    socket = new WebSocket(`/websocket/yordle/${data.gameKey}/ws?client_id=${clientId}`);
    socket.onmessage = (message) => {
      let ev = JSON.parse(message.data)

      if (ev.state != undefined) {
        updateState(ev.state)
      }
    }

    socket.onclose = (event) => {
      console.log("closing", event)
      if (closing) {
        return
      }
      
      console.log("socket closed", event)
      if (event.reason === "game_over") {
        console.log("game over")
        const interval = setInterval(() => {
          console.log("fetching new state")
          if (state === GameState.OVER) {
            console.log("clearing interval")
            clearInterval(interval)
            return
          }

          fetch(`/api/wordle/${data.gameKey}`, {
            method: "GET",
            headers: {
              "clientid": clientId
            }
          }).then(resp => resp.json()).then((respData) => {
            updateState(respData.state)
          }).catch((err) => {
            console.log(err)
            clearInterval(interval)
          })
        }, 1000)
      } else {
        goto("/")
      }
    }

  } catch (error) {
      console.error(error);
  }
}


/**
 * @type {WebSocket} socket
*/
onMount(() => {
  clientId = data.clientId
  currentGuess = ""
  answerLen = 10
  console.log("game key", data.gameKey)
  gameKey = data.gameKey

  connect()
 
  console.log('mounted');
  return () => {
    closing = true
    if (socket) {
      socket.close()
    }
  }
});

onDestroy(() => {
  if (socket) {
    socket.close()
  }
})

/**
 * handles key press events
 * @param {any} event
 */
function handleKeyPress(event) {
  if (state === GameState.ACTIVE) {
    const letter = event.key.toUpperCase();
    console.log(letter)
    if (letter === "BACKSPACE") {
      removeLetter()
    } else if (letter === "ENTER") {
      submitAnswer()
    } else if (letter >= 'A' && letter <= 'Z') {
      addLetter(letter[0]);
    }
  }
}

function leaveGame() {
  if (socket) {
    socket.close()
  }

  goto("/")
}

/**
 * Creates a new action message to send
 * @param {string} action
 * @param {any} messageData
 */
function newActionMessage(action, messageData) {
  return JSON.stringify({"player_input": {"action": action, "data": messageData}})
}

function submitAnswer() {
  if (socket && isActive()) {
    socket.send(newActionMessage("SUBMIT", null))
  }
}

function startGame() {
  if (socket && state === GameState.WAITING) {
    socket.send(newActionMessage("START", null))
  }
}

function isActive() {
  return state === GameState.ACTIVE
}

/**
 * 
 * @param {string} letter
 */
function addLetter(letter) {
  console.log("adding", letter)
  if (socket && isActive()) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "ADD", "data": letter}}
    socket.send(newActionMessage("ADD", letter))
  }
}

function removeLetter() {
  console.log("removing")
  if (socket && isActive()) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "BACKSPACE"}}
    socket.send(newActionMessage("BACKSPACE", null))
  }
}
</script>
