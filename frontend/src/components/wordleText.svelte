<div class="wordle-box">
    {#each text.split('') as character, index}
      <div class="wordle-letter" style={colorMap.length > 0 ? `background-color: var(--background-color); color: ${colorMap[index] || 'black'}` : ''}>{character}</div>
    {/each}
    
    {#each Array(maxLetters - text.length) as _}
      <div class="wordle-letter">_</div>
    {/each}
</div>

<style>
  .wordle-box {
    display: flex;
    justify-content: center;
  }

  .wordle-letter {
    font-family: 'Roboto', sans-serif;
    display: inline-block;
    margin-right: 10px;
    padding: 5px;
    border: 1px solid white;
    width: 20px; /* Set a fixed width */
    height: 20px; /* Set a fixed height */
    text-align: center; /* Center the text horizontally */
    line-height: 20px; /* Center the text vertically */
  }
</style>

<script>
    import { onMount } from "svelte";


  onMount(() => {
    if (maxLetters === undefined) {
      maxLetters = text.length
    }
  })

  
  /**
   * @typedef {Object} Props
   * @property {string} [text]
   * @property {number} [maxLetters]
   * @property {Array<string>} [colorMap]
   */

  /** @type {Props} */
  let { text = "", maxLetters = $bindable(10), colorMap = [] } = $props();
</script>