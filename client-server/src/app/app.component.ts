import { Component, OnInit } from '@angular/core';
import { UserService } from './_services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private role: string = 'BU';
  isLoggedIn = false;
  showROBoard = false;
  username?: string;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    if (!document.cookie.split('; ').find(row => row.startsWith('csrftoken'))) {
      this.userService.setCSRFToken().subscribe(
        data => {
        },
        err => {
        }
      )
    }
  }
}
