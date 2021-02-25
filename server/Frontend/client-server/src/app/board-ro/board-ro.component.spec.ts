import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardROComponent } from './board-ro.component';

describe('BoardROComponent', () => {
  let component: BoardROComponent;
  let fixture: ComponentFixture<BoardROComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BoardROComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardROComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
