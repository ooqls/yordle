
<div class="hint-box">
  {#each entries as entry}
    <div class="hint-entry">
      <WordleText maxLetters={entry.guess.length} text={entry.guess} colorMap={entry.colors} />
    </div>
    {/each}

</div>

<style>
  .hint-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Change this to flex-start */
    border-radius: 8px;
    padding: 16px;
    max-height: 200px;
    min-height: 200px;
    overflow-y: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .hint-entry {
    margin-top: 8px;
  }

  .hint-box::-webkit-scrollbar {
    display: none;
  }

</style>

<script>
  import WordleText from "./wordleText.svelte";
  import { Entry } from './types'

  /**
   * @type {Array<Entry>} entries
   */
  export let entries = []
</script>