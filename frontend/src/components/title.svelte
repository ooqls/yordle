<svelte:window  onresize={() => { updateTitle(window) }} />
<div class="title">
<h1>{ expandedTitle }</h1>
</div>

<style>
  .title {
    font-family: 'Roboto', sans-serif;
    text-align: center;
  }
</style>
<script>
    import { onMount } from "svelte";

  let vowels = ['A', 'E', 'I', 'O', 'U'];

  let vowelIndex = -1;
  /**
   * @typedef {Object} Props
   * @property {string} [title]
   */

  /** @type {Props} */
  let { title = $bindable("") } = $props();
  let expandedTitle = $state("");
  let expandLetter = '';
  let consanantsLen = 0;

  onMount(() => {
    title = title.toUpperCase()
    for(let i = 0; i < title.length; i++) {
      if(vowels.includes(title[i])) {
        if (expandLetter === '') {
          vowelIndex = i;
          expandLetter = title[i];
        }
      } else {
        consanantsLen += 1
      }
    }


    if (expandLetter === '') {
      vowelIndex = Math.floor((title.length - 1) / 2)
      expandLetter = title[Math.floor((title.length - 1) / 2)];
    }

    expandedTitle = title
    updateTitle(window)
  })

    /**
   * updates the title based on the window size
   * @param {Window} window
   */
   function updateTitle(window) {
    expandedTitle = title.substring(0, vowelIndex) + expandLetter.repeat(window.innerWidth / 27 - consanantsLen) + title.substring(vowelIndex+1, title.length);
  }
</script>