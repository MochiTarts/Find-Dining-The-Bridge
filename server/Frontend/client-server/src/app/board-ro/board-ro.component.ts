import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-board-ro',
  templateUrl: './board-ro.component.html',
  styleUrls: ['./board-ro.component.scss']
})
export class BoardROComponent implements OnInit {
  content?: string;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getROBoard().subscribe(
      data => {
        this.content = data;
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    );
  }
}