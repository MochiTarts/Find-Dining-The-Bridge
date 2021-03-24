import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-filterlist-card',
  templateUrl: './filterlist-card.component.html',
  styleUrls: ['./filterlist-card.component.scss'],
})
export class FilterlistCardComponent implements OnInit {
  @Input() category: string;
  @Input() subcategories: string[];
  @Input() length: number;

  @Output() events: EventEmitter<any> = new EventEmitter<any>();

  checkMap: boolean[] = new Array(length);

  constructor() {}

  ngOnInit(): void {
    for (let i = 0; i < this.length; i++) {
      this.checkMap.push(false);
    }
  }

  sendList() {
    this.events.emit(this.checkMap);
  }
}
