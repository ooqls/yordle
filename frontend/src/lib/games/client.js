class PlayerClient {

  /**
   * 
   * @param {String} gameKey 
   */
  constructor(gameKey) {
    this.gameKey = gameKey
  }

  connect() {
    this.socket = new WebSocket(`ws://websocket/play?game_key=${this.gameKey}`)
  }

  /**
   * 
   * @param {String} letter 
   */
  AddLetter(letter) {
    if (this.socket) 
    this.socket?.send
  }
}