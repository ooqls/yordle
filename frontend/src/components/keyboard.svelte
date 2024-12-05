<div class="keyboard">
  {#each rows as row}
  <div class="keyboard-row">
    {#each row as ch}
      {#if ch === "BACKSPACE"}
      <button disabled={disabled} class="key" on:click={() => backspace()}>{ch}</button>
      {:else if ch === "ENTER"}
      <button disabled={disabled} class="key" on:click={() => enter()}>{ch}</button>
      {:else}
      <button disabled={disabled} class="key" on:click={() => onKeyPress(ch)}>{ch}</button>
      {/if}
    {/each}
  </div>
  {/each}
</div>

<style>
    .keyboard {
        font-family: 'Roboto', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 800px;
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
      .keyboard {
        flex-direction: column;
        align-items: center;
      }

      .keyboard-row {
        justify-content: center;
      }
    }
</style>

<script>
  export let backspace = () => {}
  export let enter = () => {}

  export let onKeyPress = (ch) => {}
  export let disabled = false

  let rows = [
  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
  ["Z", "X", "C", "V", "B", "N", "M"],
  ["BACKSPACE", "ENTER"]
]
</script>