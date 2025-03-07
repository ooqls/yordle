<svelte:window on:keypress={handleKeyPress} />
<div>
  <div class="game-container">
    <Title title="yordle"></Title>
    <div class="button-container">
      <h2>{data.gameKey}</h2>
      <Button onclick={() => { leaveGame() }}>Leave</Button>
      {#if curState == GameState.ACTIVE}
      <h2>Guesses Left: {displayGuesses}</h2>
      {/if}
    </div>
    {#if curState === GameState.ACTIVE}
    <div class="wordle-container">
      <div class="wordle-text-container">
        <div class="guess-container">         
          <WordleText maxLetters={answerLen} text={currentGuess} />
        </div>
        <WordleHint entries={guessHistory} />
      </div>
      <div class="keyboard-container">
        <Keyboard enter={submitAnswer} backspace={removeLetter} onKeyPress={addLetter} disabled={curState !== GameState.ACTIVE} />
      </div>
    </div>
    {:else if curState === GameState.OVER}
    <div class="summary">
      {#if isWon}
      <h1>Correct!</h1>
      {:else}
      <h1>Incorrect</h1>
      {/if}
    </div>
    {:else if curState === GameState.INITIALIZING}
    <CircularProgress style="height: 32px; width: 32px;" indeterminate />
    {/if}
  </div>
</div>

<style>
  .button-container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }

  .wordle-container {
    display: grid;
    align-items: center;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    grid-template-rows: repeat(5, minmax(0, 1fr));
  }


  @media (max-width: 600px) {

    .wordle-container {
      display: flex;
      flex-direction: column;
    }

    .keyboard-container {
      width: 100%;
    }

    .game-container {
      grid-template-rows: 1fr 1fr 4fr;
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
  .keyboard-container {
    grid-area: 2 / 1 / 6 / 6;
    display: flex;
    justify-content: center;
  }

  .game-container {
    display: grid;
    grid-template-rows: 1fr 1fr 4fr;
    align-items: center;
  }
</style>

<script>
import CircularProgress from '@smui/circular-progress';


import { onMount,onDestroy, setContext, getContext } from "svelte";
import Title from "$components/title.svelte"
import WordleText from "$components/wordleText.svelte";
import WordleHint from "$components/wordleHint.svelte";
import Keyboard from "$components/keyboard.svelte";
import Button from "@smui/button";
import { Entry } from "$components/types"
import { goto } from "$app/navigation";



/**
 * @type {Object<string, any>}
 */
let { data } = $props()

/**
 * @type {string|undefined}
 */
let clientId = $state("")

/**
 * @type {string}
 */
let currentGuess = $state("")

/**
 * @type {number} length of the answer
 */
let answerLen = $state(10)

/**
 * @type {Entry[]}
*/
let guessHistory = $state([])

/**
 * @type {boolean} determines whether or not the last submition was correct
 */
let isWon = $state(false)

/**
 * @type {number} number of guesses left
 */
let guessesLeft = $state(0)

/**
 * @type {string} display of guesses left
 */
let displayGuesses = $state("")

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
let curState = $state(GameState.WAITING)

/**
 * @type {WebSocket} socket
 */
let socket;
let closing = false



/**
 * updates the current state
 * @param {Object<string, any>} new_state
 */
function updateState(new_state) {
  if (clientId === undefined) {
    return
  }
  
  if (new_state.answer_len !== undefined) {
    answerLen = new_state.answer_len
  }

  if (new_state.guess_history != undefined) {
    guessHistory = new_state.guess_history.guesses
  }

  if (new_state.guesses_left != undefined) {
    guessesLeft = new_state.guesses_left
    displayGuesses = "🪨".repeat(guessesLeft)
  }

  if (new_state.state != undefined) {
    curState = new_state.state
  }

  if (new_state.current_guess != undefined) {
    currentGuess = new_state.current_guess
  }
}

function connect() {
  try {
    socket = new WebSocket(`/websocket/classicyordle/${data.gameKey}/ws?client_id=${clientId}`);
    socket.onmessage = (message) => {
      let ev = JSON.parse(message.data)

      if (ev.state != undefined) {
        updateState(ev.state)
      }
    }

    socket.onclose = (event) => {
      if (closing) {
        return
      }
      
      if (event.reason === "game_over") {
        const interval = setInterval(() => {
          if (curState === GameState.OVER) {
            clearInterval(interval)
            return
          }

          fetch(`/api/classicyordle/${data.gameKey}`, {
            method: "GET",
            headers: clientId ? { "clientid": clientId } : {}
          }).then(resp => resp.json()).then((respData) => {
            updateState(respData.state)
          }).catch((err) => {
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
  console.log(clientId)
  currentGuess = ""
  answerLen = 10

  connect()
 
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
  if (curState === GameState.ACTIVE) {
    const letter = event.key.toUpperCase();
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

function isActive() {
  return curState === GameState.ACTIVE
}

/**
 * 
 * @param {string} letter
 */
function addLetter(letter) {
  if (socket && isActive()) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "ADD", "data": letter}}
    socket.send(newActionMessage("ADD", letter))
  }
}

function removeLetter() {
  if (socket && isActive()) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "BACKSPACE"}}
    socket.send(newActionMessage("BACKSPACE", null))
  }
}
</script>
