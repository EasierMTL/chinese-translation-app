/**
 * https://stackoverflow.com/questions/31626231/custom-error-class-in-typescript
 */
class HTTPError extends Error {
  public status: number;
  public statusText: string;
  constructor(status: number, statusText: string) {
    super(`${status}: ${statusText}`);
    // Set the prototype explicitly.
    Object.setPrototypeOf(this, HTTPError.prototype);
    this.status = status;
    this.statusText = statusText;
  }
}

export { HTTPError };
