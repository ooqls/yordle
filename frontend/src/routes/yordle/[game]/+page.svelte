<svelte:window  on:keydown={handleKeyPress} />
<head>
  <style>
    .keyboard {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 20px;
      width: 100%;
    }
    .keyboard-row {
      display: flex;
      justify-content: center;
      width: 100%;
    }
    .key {
      flex: 1;
      max-width: 100px;
      max-height: 100px;
      margin: 5px;
      text-align: center;
      line-height: 40px;
      border: 1px solid #ccc;
      border-radius: 5px;
      cursor: pointer;
      user-select: none;
      transition: background 0.3s;
      color: #338;
    }
    .key:hover {
      background: #f0f0f0;
    }
    .key:active {
      background: #ccc;
    }
    @media (max-width: 600px) {
      .key {
        max-width: 30px;
        height: 30px;
        line-height: 30px;
        margin: 3px;
      }
    }
    .header {
      text-align: center;
      margin-top: 20px;
    }
    .yordle-container {
      display: grid;
      align-items: center;
      grid-template-rows: 1fr 1fr 4fr;
    }

    .game-container {
      display: grid;
      grid-template-rows: 1fr 1fr 4fr;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="game-container">
    <Title title="yordle"></Title>
    <Button href="/">Back</Button>
    <div class="yordle-container">
      <YordleText maxLetters={answerLen} text={currentGuess}></YordleText>
      <LinearProgress progress={correctPercent}></LinearProgress>
      <div class="keyboard">
        <div class="keyboard-row">
          <button class="key" on:click={() => addLetter('Q')}>Q</button>
          <button class="key" on:click={() => addLetter('W')}>W</button>
          <button class="key" on:click={() => addLetter('E')}>E</button>
          <button class="key" on:click={() => addLetter('R')}>R</button>
          <button class="key" on:click={() => addLetter('T')}>T</button>
          <button class="key" on:click={() => addLetter('Y')}>Y</button>
          <button class="key" on:click={() => addLetter('U')}>U</button>
          <button class="key" on:click={() => addLetter('I')}>I</button>
          <button class="key" on:click={() => addLetter('O')}>O</button>
          <button class="key" on:click={() => addLetter('P')}>P</button>
        </div>
        <div class="keyboard-row">
          <button class="key" on:click={() => addLetter('A')}>A</button>
          <button class="key" on:click={() => addLetter('S')}>S</button>
          <button class="key" on:click={() => addLetter('D')}>D</button>
          <button class="key" on:click={() => addLetter('F')}>F</button>
          <button class="key" on:click={() => addLetter('G')}>G</button>
          <button class="key" on:click={() => addLetter('H')}>H</button>
          <button class="key" on:click={() => addLetter('J')}>J</button>
          <button class="key" on:click={() => addLetter('K')}>K</button>
          <button class="key" on:click={() => addLetter('L')}>L</button>
        </div>
        <div class="keyboard-row">
          <button class="key" on:click={() => addLetter('Z')}>Z</button>
          <button class="key" on:click={() => addLetter('X')}>X</button>
          <button class="key" on:click={() => addLetter('C')}>C</button>
          <button class="key" on:click={() => addLetter('V')}>V</button>
          <button class="key" on:click={() => addLetter('B')}>B</button>
          <button class="key" on:click={() => addLetter('N')}>N</button>
          <button class="key" on:click={() => addLetter('M')}>M</button>
          <button class="key" on:click={() => removeLetter()}>del</button>
        </div>
      </div>
    </div>
  </div>
</body>

<script>
import websocketStore from "svelte-websocket-store";
import LinearProgress from '@smui/linear-progress';

import { onMount, setContext, getContext } from "svelte";
import Title from '../../../components/title.svelte'
import YordleText from "../../../components/yordleText.svelte";
import Button from "@smui/button";
export let data;
let currentGuess = ""
let answerLen = 10
let correctPercent = 0.0

/**
 * @type {WebSocket} socket
 */
let socket;


/**
 * updates the current guess
 * @param {string} guess
 */
let updateGuess = (guess) => {
  currentGuess = guess
}

/**
 * @type {WebSocket} socket
*/
onMount(() => {
  let clientId = data.clientId
  currentGuess = ""
  answerLen = 10

  try {
    socket = new WebSocket(`/websocket/play?game_key=${data.game_key}&client_id=${clientId}`);
    socket.onmessage = (message) => {
      console.log(message)
      let ev = JSON.parse(message.data)
      if (ev.state != undefined) {
        updateGuess(ev.state.current_guess)
        if (ev.state.answer_len != undefined) {
          answerLen = ev.state.answer_len
        }

        if (ev.state.correct_percent != undefined) {
          correctPercent = ev.state.correct_percent
          console.log(correctPercent)
        }
      }
    }

  } catch (error) {
      console.log(error);
  }
    console.log('mounted');
    return () => {
      socket.close()
    }
});

/**
 * handles key press events
 * @param {any} event
 */
function handleKeyPress(event) {
  const letter = event.key.toUpperCase();
  console.log(letter)
  if (letter === "BACKSPACE") {
    removeLetter()
  } else if (letter >= 'A' && letter <= 'Z') {
    addLetter(letter[0]);
  }
}

/**
 * 
 * @param {string} letter
 */
function addLetter(letter) {
  console.log("adding", letter)
  if (socket) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "ADD", "data": letter}}
    socket.send(JSON.stringify({"game_key": data.game_key, "player_input": {"action": "ADD", "data": letter}}))
  }
}

function removeLetter() {
  console.log("removing")
  if (socket) {
    // $socket = {"game_key": data.game_key, "player_input": {"action": "BACKSPACE"}}
    socket.send(JSON.stringify({"game_key": data.game_key, "player_input": {"action": "BACKSPACE"}}))
  }
}
</script>
