import { Injectable } from '@angular/core';
import { SocialAuthService } from 'angularx-social-login';

const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';
const AUTH_KEY = 'auth-external';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {
  RO: boolean = false;

  constructor(private socialAuth: SocialAuthService) {
    // Sets RO boolean if user is logged in with role of RO
    if (this.getUser() != {} && this.getUser()['role'] == 'RO') {
      this.RO = true;
    }
  }

  /**
   * Sets the 3rd party provider to sessionStorage
   * 
   * @param provider - the 3rd party provider
   */
  setProvider(provider: string) {
    window.sessionStorage.removeItem(AUTH_KEY);
    if (provider) {
      window.sessionStorage.setItem(AUTH_KEY, provider);
    }
  }

  /**
   * Retrieves the 3rd party provider from sessionStorage
   * @returns the 3rd party provider string
   */
  getProvider() {
    return window.sessionStorage.getItem(AUTH_KEY);
  }

  /**
   * Graceful sign out of the logged in user (sign out 3rd party if provider is not present)
   */
  signOut(): void {
    window.sessionStorage.clear();
    if (this.getProvider()) {
      this.socialAuth.signOut();
      this.setProvider('');
    }
  }

  /**
   * Updates user object and access token in sessionStorage
   * @param token - the user's access token
   */
  public updateTokenAndUser(token: string): void {
    this.saveToken(token);
    // decode the token to get the user object
    const token_parts = token.split(/\./);
    const user = JSON.parse(window.atob(token_parts[1]));
    //var token_expires = new Date(token_decoded.exp * 1000);
    //var username = token_decoded.username;
    user['token'] = token;
    this.saveUser(user);

  }

  /**
   * Saves access token to sessionStorage
   * @param token - the user's access token
   */
  public saveToken(token: string): void {
    window.sessionStorage.removeItem(TOKEN_KEY);
    window.sessionStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Retrieves the access token from sessionStorage
   * @returns the access token from sessionStorage
   */
  public getToken(): string | null {
    return window.sessionStorage.getItem(TOKEN_KEY);
  }

  /**
   * Saves the user object to sessionStorage
   * @param user - the current user object
   */
  public saveUser(user: any): void {
    this.RO = user.role == "RO";
    window.sessionStorage.removeItem(USER_KEY);
    window.sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Retrieves the user from sessionStorage
   * @returns the user object from sessionStorage
   */
  public getUser(): any {
    const user = window.sessionStorage.getItem(USER_KEY);

    if (user) {
      return JSON.parse(user);
    }

    return {};
  }
}
