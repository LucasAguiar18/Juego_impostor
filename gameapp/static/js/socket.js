const socket = io();

// probar conexión
socket.on("connect", () => {
    console.log("✅ Conectado al servidor");
});

socket.on("disconnect", () => {
    console.log("❌ Desconectado del servidor");
});

document.getElementById("joinBtn")?.addEventListener("click", () => {
    const room = "sala1"; // temporal, después será dinámico
    socket.emit("join_room", { room: room });
});

socket.on("player_joined", (data) => {
    console.log(data.msg);
});
