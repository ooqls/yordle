class PlayerScore {
  /**
   * 
   * @param {Number} multiplier 
   * @param {Number} score 
   */
  constructor(multiplier, score) {
    this.displayMultiplier = multiplier
    this.score = score
  }

  /**
   * 
   * @param {Number} points 
   */
  addPoints(points) {
    this.score += points
  }

  /**
   * 
   * @param {Number} multiplier 
   */
  setDisplayedMultiplier(multiplier) {
    this.displayMultiplier = multiplier
  }

}