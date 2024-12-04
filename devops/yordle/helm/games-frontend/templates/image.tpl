{{ define "frontend-image" -}}
{{ .Values.repo }}/{{ .Values.image }}:{{ .Values.tag }}
{{ end }}