

import { ProdItem } from "@/types/ProdItem";
import "./style.css"
import Link from "next/link";

type Props = {
    prodItem: ProdItem
}

const ProdCard = ({ prodItem }: Props) => {
    // style={{width:`${prodItem.rating.rate * 20}%`}}
    return (
        <div className="proditem">
            <div className="proditem__img-box">
                <Link href={`/${prodItem.id}`}>
                    <img src={prodItem.image} alt="" className="proditem__img" />
                </Link>

                <div className="proditem__rating">
                    <div className="proditem__stars">
                        <div className="proditem__stars-empty"></div>
                        <div className="proditem__stars-full" style={{ width: `${prodItem.rating.rate * 20}%` }}></div>
                    </div>
                    <p className="proditems__rewquant">{prodItem.rating.count} отзывов</p>
                </div>
            </div>


            <Link className="proditem__title" href={`/${prodItem.id}`}>
                <p >{prodItem.title}</p>
            </Link>
            <strong className="proditem__price">{prodItem.price}</strong>
        </div>
    );
}

export default ProdCard;