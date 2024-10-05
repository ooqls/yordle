<div class="yordle-box">
  
  {#each text as character}
    <div class="yordle-letter">{character}</div>
  {/each}
    
    {#each Array(maxLetters - text.length) as _}
      <div class="yordle-letter">_</div>
    {/each}
</div>

<style>
  .yordle-box {
    display: flex;
    justify-content: center;
  }

  .yordle-letter {
    display: inline-block;
    margin-right: 10px;
    padding: 5px;
    border: 1px solid white;
  }
</style>

<script>
  export let text = ""
  export let maxLetters = 10
</script>