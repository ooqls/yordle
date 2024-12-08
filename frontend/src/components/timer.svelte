<div class="timer">
  Time Left: {displaySeconds}
</div>

<style>
  .timer {
    font-family: 'Roboto', sans-serif;
    font-size: large;
  }
</style>

<script>
  import { run } from 'svelte/legacy';

  import { onMount } from "svelte";

  /**
   * @typedef {Object} Props
   * @property {number} [secondsLeft]
   */

  /** @type {Props} */
  let { secondsLeft = 0 } = $props();
  let displaySeconds = $state("")
  run(() => {
    displaySeconds = Math.ceil(secondsLeft).toString().padStart(4, "0");
  });
  // let interval = setInterval(() => {
  //   if (secondsLeft <= 0) {
  //     secondsLeft = 0
  //     displaySeconds = "0000"
  //     clearInterval(interval);
  //   }
    
  // }, 1000)
  
</script>