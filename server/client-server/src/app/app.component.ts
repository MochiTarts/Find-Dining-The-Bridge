import {Component, OnInit} from '@angular/core';
import {UserService} from './user.service';
import {throwError} from 'rxjs';
 
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
 
  title = 'client-server';
  /**
   * An object representing the user for the login form
   */
  public user: any;
 
  constructor(public userService: UserService) { }
 
  ngOnInit() {
    this.user = {
      username: '',
      password: ''
    };
  }
 
  login() {
    this.userService.login({'username': this.user.username, 'password': this.user.password});
  }
 
  refreshToken() {
    this.userService.refreshToken();
  }
 
  logout() {
    this.userService.logout();
  }
 
}