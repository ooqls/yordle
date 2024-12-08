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

  /**
   * @typedef {Object} Props
   * @property {any} [players]
   * @property {string} [currentPlayerId]
   */

  /** @type {Props} */
  let { players = {}, currentPlayerId = "" } = $props();

</script>