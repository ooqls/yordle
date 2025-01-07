  
  
class Game {
  /**
   * 
   * @param {String} name 
   * @param {String} displayName 
   * @param {String} key 
   */
  constructor(name, displayName, key) {
    this.name = name;
    this.display_name = displayName;
    this.key = key;
  }
}

class GameList {
    /**
     * @param {Game[]} active_games
     * @param {Game[]} game_list
     */
    constructor(active_games, game_list) {
      this.active_games = active_games;
      this.game_list = game_list
    }
}

  export {Game, GameList}