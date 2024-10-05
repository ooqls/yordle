{{- define "backend-image" -}}
{{ .Values.repo }}/{{ .Values.image }}:{{ .Values.tag }}
{{- end }}