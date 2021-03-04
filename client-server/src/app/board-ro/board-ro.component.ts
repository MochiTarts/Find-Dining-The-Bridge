import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';
import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from '../_services/token-storage.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-board-ro',
  templateUrl: './board-ro.component.html',
  styleUrls: ['./board-ro.component.scss']
})
export class BoardROComponent implements OnInit {
  content?: string;

  constructor(private router: Router, private authService: AuthService, private userService: UserService, private tokenStorage: TokenStorageService) { }


  ngOnInit(): void {
    const token = this.tokenStorage.getToken();
    //console.log(token);
    if (token && this.tokenStorage.getUser().role == 'RO') {
      this.userService.getROBoard().subscribe(
        data => {
          this.content = data;
        },
        err => {
          console.log(err);
          this.content = err.error.message;
        }
      );
    } else {
      this.router.navigateByUrl('/');
    }
  }
}