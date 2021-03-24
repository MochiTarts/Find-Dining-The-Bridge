import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-owner-card',
  templateUrl: './owner-card.component.html',
  styleUrls: ['./owner-card.component.scss'],
})
export class OwnerCardComponent implements OnInit {
  @Input() story: any;

  constructor() {}

  ngOnInit(): void {}
}
