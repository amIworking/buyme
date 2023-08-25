
import { ProdItem } from "@/types/ProdItem"
import "./style.css"
import ProdCard from "@/components/prodCard/ProdCard"



async function getData() {
    const response = await fetch('https://fakestoreapi.com/products')
    return response.json()
}



const Catalog = async () => {
    const prodItems = await getData()
    const categories: Array<string> = []
    prodItems.forEach((item: ProdItem) => {
        if (!categories.includes(item.category)) categories.push(item.category)
    })

    return (
        <main className="catalog">
            <div className="container">
                <div className="main__catalog">

                    <h1 className="catalog__title">Каталог</h1>
                    <div className="catalog__cards">
                        {prodItems.map((item: ProdItem, id: number) => {
                            return <ProdCard prodItem={item} key={id} />
                        })}
                    </div>

                </div>
            </div>
        </main>
    );
}

export default Catalog;