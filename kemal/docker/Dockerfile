# Stage 1: Development environment
FROM golang:1.22-alpine AS builder

# Install git and essential build tools
RUN apk add --no-cache git make gcc musl-dev

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application with optimizations
# CGO_ENABLED=0 creates a static binary
# -ldflags="-w -s" reduces binary size by removing debug information
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s" \
    -o /go/bin/app \
    ./cmd/main.go

# Stage 2: Production environment
FROM alpine:3.19

# Add CA certificates for HTTPS
RUN apk --no-cache add ca-certificates tzdata

# Create non-root user for security
RUN adduser -D -g '' appuser

# Set working directory
WORKDIR /app

# Copy binary from builder
COPY --from=builder /go/bin/app .

# Copy config files if needed
COPY --from=builder /app/config ./config

# Use non-root user
USER appuser

# Expose application port
EXPOSE 8080

# Set health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Run the application
CMD ["./app"]
