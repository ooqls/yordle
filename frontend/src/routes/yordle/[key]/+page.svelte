<script>
    import CircularProgress from "@smui/circular-progress";
    import { onMount, onDestroy, setContext, getContext } from "svelte";
    import ButtonCheckMark from "$components/ButtonCheckMark.svelte";

    import Title from "$components/title.svelte";
    import WordleText from "$components/wordleText.svelte";
    import WordleHint from "$components/wordleHint.svelte";
    import Countdown from "$components/countdown.svelte";
    import Keyboard from "$components/keyboard.svelte";
    import Button from "@smui/button";
    import { Entry } from "$components/types";
    import Scoreboard from "$components/scoreboard.svelte";
    import Timer from "$components/timer.svelte";
    import { goto } from "$app/navigation";
    import {flip} from "svelte/animate";
    import 'iconify-icon'

    let { data } = $props();

    /**
     * @type {string|undefined}
     */
    let clientId = $state("");

    let currentGuess = $state("");
    /**
     * @type {Object<string, string>}
     */
    let allCurrentGuesses = $state({});

    let currentIndex = $state(0);

    /**
     * @type {Object<string, number>}
     */
    let currentScores = $state({});
    let answerLen = $state(10);

    let isAdmin = $state(false);

    /**
     * @type {Object<string, number>}
     */
    let allAnswerLen = $state({});

    let score = $state(0);

    /**
     * @type {Entry[]}
     */
    let guessHistory = $state([]);

    const GameState = {
        ACTIVE: "State.ACTIVE",
        OVER: "State.OVER",
        WAITING: "State.WAITING",
        STARTING: "State.STARTING",
        INITIALIZING: "State.INITIALIZING",
    };
    /**
     * @type {String}
     */
    let curState = $state(GameState.WAITING);
    let secondsLeft = $state(30);

    /**
     * @type {WebSocket} socket
     */
    let socket;
    let closing = false;

    /**
     * updates the current guess
     * @param {string} guess
     */
    let updateGuess = (guess) => {
        currentGuess = guess;
    };

    /**
     * updates the current state
     * @param {Object<string, any>} new_state
     */
    function updateState(new_state) {
        if (clientId === undefined) {
            return;
        }


        if (new_state.answer_len !== undefined) {
            allAnswerLen = new_state.answer_len;
            if (allAnswerLen[clientId] !== undefined) {
                answerLen = allAnswerLen[clientId];
            }
        }

        if (new_state.is_admin !== undefined) {
            isAdmin = new_state.is_admin;
        }

        if (new_state.scores !== undefined) {
            if (
                clientId !== undefined &&
                new_state.scores[clientId] !== undefined
            ) {
                score = new_state.scores[clientId];
            }
            currentScores = new_state.scores;
        }

        if (new_state.guess_history != undefined) {
            guessHistory = new_state.guess_history.guesses;
        }

        if (new_state.time_left != undefined) {
            secondsLeft = new_state.time_left;
        }

        if (new_state.state != undefined) {
            curState = new_state.state;
        }

        if (
            new_state.word_index != undefined &&
            clientId in new_state.word_index
        ) {
            currentIndex = new_state.word_index[clientId];
        }

        if (new_state.current_guess != undefined) {
            allCurrentGuesses = new_state.current_guess;
            if (
                clientId != undefined &&
                allCurrentGuesses[clientId] != undefined
            ) {
                updateGuess(allCurrentGuesses[clientId]);
            }
        }
    }

    function connect() {
        try {
            socket = new WebSocket(
                `/websocket/yordle/${data.gameKey}/ws?client_id=${clientId}`,
            );
            socket.onmessage = (message) => {
                let ev = JSON.parse(message.data);

                if (ev.state != undefined) {
                    updateState(ev.state);
                }
            };

            socket.onclose = (event) => {
                if (closing) {
                    return;
                }

                if (event.reason === "game_over") {
                    const interval = setInterval(() => {
                        if (curState === GameState.OVER) {
                            clearInterval(interval);
                            return;
                        }

                        fetch(`/api/wordle/${data.gameKey}`, {
                            method: "GET",
                            headers: clientId
                                ? {
                                      clientid: clientId,
                                  }
                                : {},
                        })
                            .then((resp) => resp.json())
                            .then((respData) => {
                                updateState(respData.state);
                            })
                            .catch((err) => {
                                clearInterval(interval);
                            });
                    }, 1000);
                } else {
                    goto("/");
                }
            };
        } catch (error) {
            console.error(error);
        }
    }

    /**
     * @type {WebSocket} socket
     */
    onMount(() => {
        clientId = data.clientId;
        currentGuess = "";
        answerLen = 10;

        connect();

        return () => {
            closing = true;
            if (socket) {
                socket.close();
            }
        };
    });

    onDestroy(() => {
        if (socket) {
            socket.close();
        }
    });

    /**
     * handles key press events
     * @param {any} event
     */
    function handleKeyPress(event) {
        if (curState === GameState.ACTIVE) {
            const letter = event.key.toUpperCase();
            if (letter === "BACKSPACE") {
                removeLetter();
            } else if (letter === "ENTER") {
                submitAnswer();
            } else if (letter >= "A" && letter <= "Z") {
                addLetter(letter[0]);
            }
        }
    }

    function leaveGame() {
        if (socket) {
            socket.close();
        }

        goto("/");
    }

    /**
     * Creates a new action message to send
     * @param {string} action
     * @param {any} messageData
     */
    function newActionMessage(action, messageData) {
        return JSON.stringify({
            player_input: { action: action, data: messageData },
        });
    }

    function submitAnswer() {
        if (socket && isActive()) {
            socket.send(newActionMessage("SUBMIT", null));
        }
    }

    function startGame() {
        if (socket && curState === GameState.WAITING) {
            console.log("sending start message");
            socket.send(newActionMessage("START", null));
        }
    }

    function isActive() {
        return curState === GameState.ACTIVE;
    }

    function copyGameKey() {
        navigator.clipboard.writeText(data.gameKey);
    }

    /**
     *
     * @param {string} letter
     */
    function addLetter(letter) {
        if (socket && isActive()) {
            // $socket = {"game_key": data.game_key, "player_input": {"action": "ADD", "data": letter}}
            socket.send(newActionMessage("ADD", letter));
        }
    }

    function removeLetter() {
        if (socket && isActive()) {
            // $socket = {"game_key": data.game_key, "player_input": {"action": "BACKSPACE"}}
            socket.send(newActionMessage("BACKSPACE", null));
        }
    }
</script>

<svelte:window on:keypress={handleKeyPress} />
<div>
    <div class="game-container">
        <Title title="yordle"></Title>
        <div class="button-container">
            <h3>
                {data.gameKey}
                <ButtonCheckMark onclick={copyGameKey} >
                    <iconify-icon style="font-size: 24px;" icon="mdi:content-copy"></iconify-icon>
                </ButtonCheckMark>
            </h3>

            <Button onclick={leaveGame}>Leave</Button>

            {#if curState == GameState.ACTIVE}
                <Timer {secondsLeft} />
                <b>Lvl: {currentIndex + 1}</b>
            {:else if curState == GameState.WAITING}
                {#if isAdmin}
                    <Button
                        onclick={() => {
                            startGame();
                        }}>Start
                    </Button>
                {:else}
                <h2>Waiting for game to start</h2>
                {/if}
            {/if}
        </div>
        {#if curState === GameState.ACTIVE}
            <div class="wordle-container">
                <div class="score-container">
                    <Scoreboard
                        currentPlayerId={clientId}
                        scores={currentScores}
                    ></Scoreboard>
                </div>
                <div class="wordle-text-container">
                    <div class="guess-container">
                        {#each Object.keys(allCurrentGuesses) as playerId}
                            {#if playerId !== clientId && allAnswerLen[playerId] !== undefined}
                                <WordleText
                                    maxLetters={allAnswerLen[playerId]}
                                    text={allCurrentGuesses[playerId]}
                                />
                            {/if}
                        {/each}
                        <WordleText
                            maxLetters={answerLen}
                            text={currentGuess}
                        />
                    </div>
                    <WordleHint entries={guessHistory} />
                </div>
                <div class="keyboard-container">
                    <Keyboard
                        enter={submitAnswer}
                        backspace={removeLetter}
                        onKeyPress={addLetter}
                        disabled={curState !== GameState.ACTIVE}
                    />
                </div>
            </div>
        {:else if curState === GameState.OVER}
            <div class="summary">
                <h1>Game Over</h1>
                <Scoreboard
                    disableMobileView={true}
                    currentPlayerId={clientId}
                    scores={currentScores}
                ></Scoreboard>
            </div>
        {:else if curState === GameState.WAITING || curState === GameState.INITIALIZING}
            <div class="lobby">
                <Scoreboard
                    disableMobileView={true}
                    currentPlayerId={clientId}
                    scores={currentScores}
                />
            </div>
        {:else if curState === GameState.STARTING}
            <Countdown delay={3} />
        <!-- {:else if curState === GameState.INITIALIZING}
            <CircularProgress
                style="height: 32px; width: 32px;"
                indeterminate
            /> -->
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

    .score-container {
        grid-area: 1 / 1 / 3 / 2;
    }

    @media (max-width: 600px) {
        .score-container {
            padding-bottom: 10px;
        }

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

    .lobby {
        display: grid;
        grid-template-rows: 1fr 1fr;
        align-items: center;
    }
    
</style>