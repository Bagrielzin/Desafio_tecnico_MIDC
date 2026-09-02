import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.component.html'
})
export class AppComponent {
  registroForm: FormGroup;
  isSubmitting = false;
  mensagem = '';
  erro = false;

  constructor(private fb: FormBuilder, private apiService: ApiService) {
    this.registroForm = this.fb.group({
      employee_name: ['', Validators.required],
      department: ['', Validators.required],
      reference_date: ['', Validators.required],
      deliveries: [0, [Validators.required, Validators.min(0)]],
      note: ['']
    });
  }

  onSubmit() {
    if (this.registroForm.valid) {
      this.isSubmitting = true;
      this.apiService.enviarRegistro(this.registroForm.value).subscribe({
        next: () => {
          this.mensagem = 'Registro salvo com sucesso!';
          this.erro = false;
          this.registroForm.reset({ deliveries: 0 });
          this.isSubmitting = false;
        },
        error: () => {
          this.mensagem = 'Erro ao salvar. Verifique a API.';
          this.erro = true;
          this.isSubmitting = false;
        }
      });
    }
  }
}