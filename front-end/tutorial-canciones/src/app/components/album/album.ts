export class Album {

    id: number;
    titulo: string;
    anio: number;
    descripcion: string;
    medio: Medio;
    usuario: number;
    interpretes: Array<string>;
    favorita : number;
    canciones: Array<Cancion>

    constructor(
        id: number,
        titulo: string,
        anio: number,
        descripcion: string,
        medio: Medio,
        usuario: number,
        interpretes: Array<string>,
        favorita: number,
        canciones: Array<Cancion>
    ){
        this.id = id,
        this.titulo = titulo,
        this.anio = anio,
        this.descripcion = descripcion,
        this.medio = medio,
        this.usuario = usuario,
        this.interpretes = interpretes,
        this.favorita = favorita,
        this.canciones = canciones
    }
}

export class Medio{
    llave: string;
    valor: number

    constructor(
        llave: string,
        valor:number
    ){
        this.llave = llave,
        this.valor = valor
    }
}

export class Cancion{
    id: number;
    titulo: string;
    minutos: number;
    segundos: number;
    interprete: string;
    favorita: number;

    constructor(
        id: number,
        titulo: string,
        minutos: number,
        segundos: number,
        interprete: string,
        favorita: number,
    ){
        this.id = id,
        this.titulo = titulo,
        this.minutos = minutos,
        this.segundos = segundos,
        this.interprete = interprete,
        this.favorita = favorita
    }
}
