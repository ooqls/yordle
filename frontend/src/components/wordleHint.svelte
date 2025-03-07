
<div class="hint-box">
  {#each entries as entry (entry.id) }
    <div animate:whizz class="hint-entry">
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
  import { cubicOut } from 'svelte/easing';

  
  /**
   * @typedef {Object} Props
   * @property {Array<Entry>} [entries]
   */

  /** @type {Props} */
  let { entries = [] } = $props();


  /**
   * 
   * @param {HTMLElement} node 
   * @param {Object} target
   */
  function whizz(node, target) {
    const dx = target.from.left - target.to.left;
    const dy = target.from.top - target.to.top;

    const d = Math.sqrt(dx * dx + dy * dy);

    return {
      delay: 0,
      duration: Math.sqrt(d) * 120,
      easing: cubicOut,
      css: (t, u) => `transform: translate(${u * dx}px, ${u * dy}px);`
    };
  }
</script>