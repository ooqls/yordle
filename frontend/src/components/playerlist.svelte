<div>
  <List>
    {#each Object.entries(players) as [key, value]}
    <Item class={key === currentPlayerId ? 'activated' : ''}>
      
    </Item>
    <Separator />
    {/each}
  </List>
</div>

<script>

  import List, { Item, Separator, Text } from '@smui/list'; 

  export let players = {}
  export let currentPlayerId = ""

</script>